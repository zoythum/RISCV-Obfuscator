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
	sd	ra,56(sp)
	sd	a2,48(sp)
	mv	a2,a0
	sd	t2,40(sp)
	addi	s0,sp,64
	sd	a2,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	mulw	s7,s2,t5
	sraw	s2,s9,s2
	andi	s9,t4,-1235
	xori	a2,s9,-1159
	slli	t4,a3,20
	sub	t3,s8,s11
	sw	zero,-36(s0)
	j	.L3
.L4:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	srlw	a6,t4,t1
	mv	ra,a5
	subw	t4,a3,t0
	sltu	t2,t0,a6
	add	sp,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(sp)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	mulh	s3,s11,s7
	mulhu	s6,s6,s3
	mulhsu	t5,a6,a7
.L3:
	lw	a5,-36(s0)
	sext.w	a4,a5
	sll	t1,s8,t2
	xor	s11,ra,s8
	slliw	a3,a7,29
	li	a5,4
	ble	a4,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	j	.L6
	slt	s11,s10,s11
	mv	t1,s5
	sltu	t6,s10,t0
	sll	t0,t1,t1
.L7:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L6:
	lw	a5,-36(s0)
	sext.w	a4,a5
	mv	ra,a4
	li	a5,4
	ble	ra,a5,.L7
.L8:
	nop
	mv	a0,sp
	ld	t2,56(a0)
	ld	s0,48(a0)
	ld	s1,40(a0)
	addi	sp,a0,64
	jr	t2
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
	addi	a5,s0,-136
	mv	ra,a5
	li	a1,25
	mv	a0,ra
	call	fill_array
	addi	a5,s0,-240
	mv	t2,t3
	li	a1,25
	mv	a0,a5
	xori	s5,s10,764
	slliw	s4,t2,30
	slli	t6,t4,3
	call	fill_array
	sw	zero,-20(s0)
	mulhsu	t1,a6,a3
	andi	t2,s8,-1572
	slt	t2,a3,s10
	j	.L10
	srlw	s11,a6,t4
	slli	s2,s11,21
	add	t3,t2,s2
.L15:
	sw	zero,-24(s0)
	j	.L11
.L14:
	sw	zero,-28(s0)
	slt	t1,t5,s8
	sraiw	a7,t0,28
	add	t4,s3,s10
	j	.L12
.L13:
	lw	a3,-28(s0)
	lw	a4,-20(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a3
	slli	a5,a5,2
	mv	ra,a5
	addi	a4,s0,-16
	add	a5,a4,ra
	lw	a3,-120(a5)
	lw	a2,-24(s0)
	lw	a4,-28(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a2
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a5,-224(a5)
	mulw	a5,a3,a5
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
	li	a5,4
	ble	a4,a5,.L13
	lw	ra,-24(s0)
	lw	sp,-20(s0)
	mv	a5,sp
	slli	a5,a5,2
	add	a5,a5,sp
	add	a5,a5,ra
	slli	sp,a5,2
	addi	a4,s0,-16
	add	a5,a4,sp
	lw	a4,-32(s0)
	sw	a4,-328(a5)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sraiw	t4,t5,19
	sltu	s3,a6,t4
	sub	s8,s7,s3
	sext.w	ra,a5
	li	a5,4
	ble	ra,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	sll	a2,t4,s2
	slt	t2,s10,s9
	mv	ra,a5
	sllw	t1,t2,a6
	sext.w	a4,ra
	li	a5,4
	ble	a4,a5,.L15
	li	a5,0
	mv	a0,a5
	mv	a1,sp
	ld	ra,344(a1)
	ld	s0,336(a1)
	addi	sp,a1,352
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
