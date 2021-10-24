	.file	"matrixMul.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	a4,s1
	sd	ra,56(sp)
	sd	t3,48(sp)
	sd	a4,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	sw	zero,-36(s0)
	j	.L3
	mulhu	t5,s10,s9
	addiw	s4,s4,-1809
	ori	t4,t0,-804
	mv	t1,ra
	mulhu	s2,t1,s10
	sltu	a6,t2,t5
	or	s7,t1,s8
.L4:
	lw	a5,-36(s0)
	slli	ra,a5,2
	slli	t2,t5,22
	sltu	a6,s10,a6
	xori	t5,s5,1283
	ld	a4,-56(s0)
	add	a5,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L3:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,4
	ble	a4,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	j	.L6
.L7:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	mv	ra,t3
	lw	a5,-36(s0)
	addiw	a5,a5,1
	slliw	t1,a1,1
	mul	a0,s8,a6
	srl	a0,ra,s5
	sw	a5,-36(s0)
	mulw	t5,s2,s7
	sltu	s3,s9,s3
	sll	s6,a2,t0
.L6:
	lw	a5,-36(s0)
	sext.w	a4,a5
	mv	ra,a4
	li	a5,4
	ble	ra,a5,.L7
.L8:
	nop
	ld	ra,56(a1)
	ld	s0,48(a1)
	ori	t1,a2,288
	sll	a3,s6,t2
	srl	a3,s8,a6
	ld	s1,40(a1)
	addi	sp,a1,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-352
	sd	ra,344(sp)
	sd	s0,336(sp)
	addi	s0,sp,352
	sw	zero,-32(s0)
	addi	ra,s0,-136
	li	a1,25
	mv	a0,ra
	call	fill_array
	addi	a5,s0,-240
	li	a1,25
	mv	a0,a5
	call	fill_array
	sw	zero,-20(s0)
	slliw	t3,s3,1
	subw	t1,t0,a2
	sllw	t0,a6,t6
	mul	a6,a2,a2
	addw	a2,s8,s4
	mulw	s7,s5,a3
	slli	s10,t4,12
	sllw	s11,t4,t4
	slt	s9,s11,s9
	j	.L10
.L15:
	sw	zero,-24(s0)
	j	.L11
.L14:
	sw	zero,-28(s0)
	j	.L12
.L13:
	lw	a3,-28(s0)
	lw	a4,-20(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a3
	slli	ra,a5,2
	addi	a4,s0,-16
	add	a5,a4,ra
	lw	sp,-120(ra)
	lw	a2,-24(s0)
	lw	a4,-28(s0)
	mv	t0,a4
	mv	a5,t0
	slli	a5,a5,2
	add	a5,a5,t0
	add	a5,a5,a2
	slli	t1,a5,2
	addi	a4,s0,-16
	add	a5,a4,t1
	lw	a5,-224(t1)
	mulw	a5,sp,a5
	sext.w	a5,a5
	lw	a4,-32(s0)
	addw	a5,a4,a5
	sw	a5,-32(s0)
	lw	a5,-28(s0)
	addiw	a5,a5,1
	sw	a5,-28(s0)
.L12:
	lw	a5,-28(s0)
	sext.w	a4,a5
	slt	a0,s8,a1
	mul	a7,t5,s9
	srl	s8,a1,s5
	li	a5,4
	ble	a4,a5,.L13
	lw	a3,-24(s0)
	lw	a4,-20(s0)
	mv	a5,a4
	mv	ra,a4
	slli	a5,a5,2
	add	a5,a5,ra
	add	a5,a5,a3
	slli	a5,a5,2
	mv	sp,a5
	addi	a4,s0,-16
	add	a5,a4,sp
	mv	t0,a5
	lw	a4,-32(s0)
	sw	a4,-328(t0)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sext.w	a4,a5
	li	a5,4
	slli	t4,a6,24
	slli	s2,t0,25
	mv	ra,a4
	mul	s10,s3,s5
	ble	ra,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	addi	a2,s9,-556
	srlw	a3,t2,a7
	slli	s6,s5,24
	sext.w	a4,a5
	li	a5,4
	ble	a4,a5,.L15
	li	a5,0
	mv	a0,a5
	ld	ra,344(sp)
	mv	t1,sp
	ld	s0,336(t1)
	addi	sp,t1,352
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
